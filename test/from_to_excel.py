import re
import pandas
import dateparser


def from_to_excel(input_, output_):
    with open(input_, "r", encoding='charmap') as d:
        data = d.readlines()
        index = 0
        db = pandas.DataFrame({
            "email_index": [index],
            "from": [data[0].split(",")[1]],
            "to": [" ".join(re.findall(r'[\w\.-]+@[\w\.-]+', data[0].split(",")[2])).lower().replace(" ", "")],
            "date_time": [dateparser.parse(data[0].split(",")[0])]
        })
        writer = pandas.ExcelWriter(output_, engine='xlsxwriter')
        db = db[["email_index", "from", "to", "date_time"]]

        for email in data:
            em_to = ''
            try:
                em_to = " ".join(re.findall(r'[\w\.-]+@[\w\.-]+', email.split(",")[2])[0]).lower().replace(" ","")
                if "-" in em_to:
                    em_to = em_to.split("-")[1]
            except:
                print(" ")

            if email != data[0]:
                new_db = pandas.DataFrame({
                    "email_index": [index],
                    "from": [", ".join(re.findall(r'[\w\.-]+@[\w\.-]+', email.split(",")[1])).lower()],
                    "to": [em_to],
                    "date_time": [dateparser.parse(email.split(",")[0])]
                })
                index += 1
                print(index)
                db = pandas.concat([db, new_db], ignore_index=True, axis=0)
                if not ", ".join(re.findall(r'[\w\.-]+@[\w\.-]+', email.split(",")[1])).lower():
                    print(email.split(",")[1])
        db.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
        worksheet = writer.sheets['Sheet1']
        (max_row, max_col) = db.shape
        column_settings = [{'header': column} for column in db.columns]
        worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
        worksheet.set_column(0, max_col - 1, 12)
        writer.save()
        print(db)


