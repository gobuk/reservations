import pandas as pd
import mariadb

# Database connection parameters
conn_params = {
    "user" : "test",
    "password" : "test",
    "host" : "localhost",
    "database" : "gch_pms"
}

# Establish a connection
connection = mariadb.connect(**conn_params)
cursor = connection.cursor()

# Get filename from user
filename = input("Enter filename: ")
reservation_df = pd.read_csv(filename + ".csv", sep=',', skiprows=1, 
                             index_col=False, encoding='windows-1252', 
                             dtype={"Booking No": str, "OTA NO": str},
                             parse_dates=["Reservation Date", "Arrival Date", 
                            "Departure Date"], dayfirst=True)

# Remove all ',' from Trx Amount
reservation_df["Trx Amount"] = reservation_df["Trx Amount"].str.replace(',','')

def insert_booking_data(reservation_df):
    """Insert booking data for csv into database"""

    previous_booking_id = 0

    for data in reservation_df.itertuples():
        if not pd.isnull(data[1]):
            booking_no = str(data[1])
            previous_booking_id = booking_no
        else:
            booking_no = data[1]

        # Retrieved booking data
        booking_date = data[12]
        bill_instruction = data[15]
        guest_name = data[4]
        booking_status = data[2]
        travel_agent = data[23]
        
        if not pd.isnull(data[24]):
            ota_no = str(data[24])    
        else:
            ota_no = data[24]

        # Retrieved room data
        room_type = data[16]
        query = f"SELECT room_type_id FROM room_type WHERE room_type = '{room_type}'"
        cursor.execute(query) 
        room_type_id = cursor.fetchone() 
        if room_type_id:
            room_type_id = room_type_id[0]
        else:
            print("Room type not found")
        arrival_date = data[18]
        departure_date = data[19]
        no_of_room = data[20]
        trx_amount = data[22]
        print(room_type_id, arrival_date, departure_date, no_of_room, trx_amount)

        nodata = pd.isnull(booking_no)
        date_format = '%Y-%m-%d'
        if nodata:
            booking_no = previous_booking_id

        if not nodata:
            # Insert booking data into booking database
            cursor.execute("INSERT IGNORE INTO booking (booking_no, booking_date,"
                        "bill_instruction, guest_name, booking_status,"
                        "travel_agent, ota_no) VALUES"
                        "(?,?,?,?,?,?,?)",
                        (booking_no, booking_date.strftime(date_format),
                        bill_instruction, guest_name, booking_status, 
                        travel_agent, ota_no))
            
        # Insert room data into rooms database
        cursor.execute("INSERT INTO rooms (no_of_room, room_type_id,"
                       "booking_no, arrival_date, departure_date,"
                       "trx_amount) VALUES"
                       "(?,?,?,?,?,?)",
                       (no_of_room, room_type_id, booking_no,
                        arrival_date.strftime(date_format), 
                        departure_date.strftime(date_format),
                        trx_amount))

# Insert data into database
insert_booking_data(reservation_df)

# Save database
connection.commit()
# freed resources
cursor.close()
connection.close()

