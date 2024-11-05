CREATE TABLE rooms (
rooms_id INT(12) AUTO_INCREMENT KEY,
no_of_room INT(3),
room_type_id INT(12),
booking_no INT(12),
arrival_date DATE,
departure_date DATE,
trx_amount FLOAT,
CONSTRAINT fk_room_type FOREIGN KEY (room_type_id) REFERENCES room_type(room_type_id),
CONSTRAINT fk_booking_no FOREIGN KEY (booking_no) REFERENCES booking(booking_no)
);