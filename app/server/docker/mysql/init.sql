-- Создаем базу данных (имя должно совпадать с MYSQL_DATABASE в docker-compose.yml)
CREATE DATABASE IF NOT EXISTS cinema_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE cinema_db;

-- ==========================================
-- 1. ПОЛЬЗОВАТЕЛИ И БЕЗОПАСНОСТЬ
-- ==========================================

CREATE TABLE USERS (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    full_name VARCHAR(255),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    is_guest BOOLEAN DEFAULT FALSE, -- Для покупок без регистрации
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE USER_2FA (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    secret VARCHAR(255) NOT NULL,
    enabled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES USERS(id) ON DELETE CASCADE
);

CREATE TABLE USER_2FA_RECOVERY_CODES (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES USERS(id) ON DELETE CASCADE
);

-- ==========================================
-- 2. КИНОТЕАТР: ФИЛЬМЫ, ЗАЛЫ, МЕСТА
-- ==========================================

CREATE TABLE MOVIES (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    duration_minutes INT NOT NULL,
    release_date DATE,
    poster_url VARCHAR(500)
);

CREATE TABLE HALLS (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(100) NOT NULL,
    rows_count INT NOT NULL,
    cols_count INT NOT NULL
);

CREATE TABLE SEATS (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    hall_id CHAR(36) NOT NULL,
    seat_row VARCHAR(10) NOT NULL, -- Может быть "A", "VIP" или просто "1"
    seat_number INT NOT NULL,
    seat_type ENUM('standard', 'vip', 'loveseat') DEFAULT 'standard',
    FOREIGN KEY (hall_id) REFERENCES HALLS(id) ON DELETE CASCADE,
    UNIQUE KEY unique_seat_in_hall (hall_id, seat_row, seat_number)
);

-- ==========================================
-- 3. РАСПИСАНИЕ И УПРАВЛЕНИЕ МЕСТАМИ (Race Condition fix)
-- ==========================================

CREATE TABLE SCREENINGS (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    movie_id CHAR(36) NOT NULL,
    hall_id CHAR(36) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    base_price INT NOT NULL, -- Цена в минимальных единицах (например, в копейках или центах)
    FOREIGN KEY (movie_id) REFERENCES MOVIES(id) ON DELETE RESTRICT,
    FOREIGN KEY (hall_id) REFERENCES HALLS(id) ON DELETE RESTRICT
);

-- ТАБЛИЦА БЛОКИРОВОК (Чтобы 2 человека не купили 1 место)
CREATE TABLE SCREENING_SEATS (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    screening_id CHAR(36) NOT NULL,
    seat_id CHAR(36) NOT NULL,
    status ENUM('free', 'locked', 'sold') DEFAULT 'free',
    locked_until TIMESTAMP NULL, -- Время, когда бронь в корзине сгорит
    locked_by_user_id CHAR(36) NULL, -- Кто сейчас держит место в корзине
    FOREIGN KEY (screening_id) REFERENCES SCREENINGS(id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES SEATS(id) ON DELETE CASCADE,
    FOREIGN KEY (locked_by_user_id) REFERENCES USERS(id) ON DELETE SET NULL,
    UNIQUE KEY unique_seat_per_screening (screening_id, seat_id)
);

-- ==========================================
-- 4. ПРОДАЖИ: БРОНИРОВАНИЕ, ОПЛАТА, БИЛЕТЫ
-- ==========================================

CREATE TABLE PROMO_CODES (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    code VARCHAR(50) UNIQUE NOT NULL,
    discount_percent INT DEFAULT 0,
    discount_amount INT DEFAULT 0,
    valid_until TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE BOOKINGS (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    screening_id CHAR(36) NOT NULL,
    promo_code_id CHAR(36) NULL,
    status ENUM('pending', 'paid', 'cancelled', 'refunded') DEFAULT 'pending',
    total_amount INT NOT NULL,
    reserved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL, -- До какого времени нужно оплатить
    paid_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES USERS(id) ON DELETE RESTRICT,
    FOREIGN KEY (screening_id) REFERENCES SCREENINGS(id) ON DELETE RESTRICT,
    FOREIGN KEY (promo_code_id) REFERENCES PROMO_CODES(id) ON DELETE SET NULL
);

CREATE TABLE BOOKING_ITEMS (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    booking_id CHAR(36) NOT NULL,
    seat_id CHAR(36) NOT NULL,
    price INT NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES BOOKINGS(id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES SEATS(id) ON DELETE RESTRICT
);

CREATE TABLE PAYMENTS (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    booking_id CHAR(36) NOT NULL,
    user_id CHAR(36) NOT NULL,
    provider VARCHAR(100) NOT NULL, -- 'Stripe', 'YooKassa', etc.
    provider_payment_id VARCHAR(255),
    amount INT NOT NULL,
    status ENUM('pending', 'success', 'failed', 'refunded') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES BOOKINGS(id) ON DELETE RESTRICT,
    FOREIGN KEY (user_id) REFERENCES USERS(id) ON DELETE RESTRICT
);

CREATE TABLE TICKETS (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    booking_item_id CHAR(36) NOT NULL UNIQUE,
    user_id CHAR(36) NOT NULL,
    ticket_code VARCHAR(100) UNIQUE NOT NULL,
    qr_code VARCHAR(500),
    is_used BOOLEAN DEFAULT FALSE,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_item_id) REFERENCES BOOKING_ITEMS(id) ON DELETE RESTRICT,
    FOREIGN KEY (user_id) REFERENCES USERS(id) ON DELETE RESTRICT
);

CREATE TABLE PRINT_REQUESTS (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    booking_id CHAR(36) NOT NULL,
    user_id CHAR(36) NOT NULL,
    status ENUM('pending', 'printed', 'failed') DEFAULT 'pending',
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES BOOKINGS(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES USERS(id) ON DELETE CASCADE
);

-- ==========================================
-- 5. ТЕСТОВЫЕ ДАННЫЕ (ЧТОБЫ БЫЛО С ЧЕМ РАБОТАТЬ)
-- ==========================================

-- Добавим один зал и фильм для старта
INSERT INTO HALLS (id, name, rows_count, cols_count) VALUES ('h1-uuid-0000', 'Главный Зал', 10, 10);
INSERT INTO MOVIES (id, title, description, duration_minutes, release_date) 
VALUES ('m1-uuid-0000', 'Интерстеллар', 'Фильм про космос', 169, '2014-11-06');

-- Добавим пару мест
INSERT INTO SEATS (id, hall_id, seat_row, seat_number, seat_type) VALUES 
('s1-uuid-0000', 'h1-uuid-0000', '1', 1, 'standard'),
('s2-uuid-0000', 'h1-uuid-0000', '1', 2, 'standard'),
('s3-uuid-0000', 'h1-uuid-0000', 'VIP', 1, 'vip');

-- Добавим один сеанс
INSERT INTO SCREENINGS (id, movie_id, hall_id, start_time, end_time, base_price) 
VALUES ('scr1-uuid-0000', 'm1-uuid-0000', 'h1-uuid-0000', '2024-12-01 19:00:00', '2024-12-01 22:00:00', 50000);