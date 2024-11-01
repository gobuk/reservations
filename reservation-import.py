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

def insert_booking_data(reservation_df):
    """Insert booking data for csv into database"""

    for data in reservation_df.itertuples():
        if not pd.isnull(data[1]):
            booking_no = str(data[1])    
        else:
            booking_no = data[1]

        booking_date = data[12]
        bill_instruction = data[15]
        guest_name = data[4]
        booking_status = data[2]
        travel_agent = data[23]
        
        if not pd.isnull(data[24]):
            ota_no = str(data[24])    
        else:
            ota_no = data[24]

        nodata = pd.isnull(booking_no)
        date_format = '%Y-%m-%d'

        if not nodata:
            cursor.execute("INSERT IGNORE INTO booking (booking_no, booking_date,"
                        "bill_instruction, guest_name, booking_status,"
                        "travel_agent, ota_no) VALUES"
                        "(?,?,?,?,?,?,?)",
                        (booking_no, booking_date.strftime(date_format),
                        bill_instruction, guest_name, booking_status, 
                        travel_agent, ota_no))
    
# Insert data into database
insert_booking_data(reservation_df)

# Save database
connection.commit()
# freed resources
cursor.close()
connection.close()

