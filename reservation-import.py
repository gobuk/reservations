import pandas as pd

# Get filename from user
filename = input("Enter filename: ")
reservation_df = pd.read_csv(filename + ".csv", sep=',', skiprows=1, 
                             index_col=False, encoding='windows-1252')
booking_no = 0
count = 0
for data in reservation_df.itertuples():
    current_booking = data[1]
    more_room = pd.isnull(current_booking)
    
    if more_room:
        # null booking no. means guest booking more than 1 room
        print(count, booking_no, more_room)
    else:
        print(count, current_booking)
        booking_no = current_booking
    
    count = count + 1


