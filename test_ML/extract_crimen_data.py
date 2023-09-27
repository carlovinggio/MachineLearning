
pdf_format = r"C:\Users\carlo\Downloads\{year}.pdf" # TODO. 
from tabula import read_pdf
from tabulate import tabulate
import pandas as pd

states = ["aguascalientes", "baja california", "baja california sur", "campeche", "chiapas", "chihuahua", "coahuila", "colima", "ciudad de mexico", "durango", "estado de mexico", "guanajuato", "guerrero", "hidalgo", "jalisco", "mexico", "michoacan", "morelos", "nayarit", "nuevo leon", "oaxaca"]
states.extend(["puebla", "queretaro", "quintana roo", "san luis potosi", "sinaloa", "sonora", "tabasco", "tamaulipas", "tlaxcala", "veracruz", "yucatan", "zacatecas"])
#reads table from pdf file
df = read_pdf(r"C:\Users\carlo\Downloads\2013.pdf",pages="3") #address of pdf file

years = [2013, 2014, 2015, 2016]
# convert month to number

converter = {
    "ENERO": "01",
    "FEBRERO": "02",
    "MARZO": "03",
    "ABRIL": "04",
    "MAYO": "05",
    "JUNIO": "06",
    "JULIO": "07",
    "AGOSTO": "08",
    "SEPTIEMBRE": "09",
    "OCTUBRE": "10",
    "NOVIEMBRE": "11",
    "DICIEMBRE": "12"
}

index_to_save = {
    "1TOTAL DE ROBOS": "total_robos",
    "2TOTAL DE LESIONES": "total_lesiones",
    "3TOTAL DE HOMICIDIOS": "total_homicidios",
    "4DELITOS PATRIMONIALES": "delitos_patrimoniales",
    "5PRIV. DE LA LIBERTAD (SECUESTRO)": "secuestro",
    "6DELITOS SEXUALES (VIOLACION)": "violacion",
    "7OTROS DELITOS": "otros_delitos",
}
dataframes = {state: pd.DataFrame({}) for state in states}
ending_page = 33
current_page = 3


def remove_char(text, char=","):
    result = []
    i = 0
    while i < len(text):
        if text[i] == char:
            i += 2  # Skip the comma and the next character
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)


for year in years:
    pdf_path = pdf_format.format(year=year)
    for state in states:
        df = read_pdf(pdf_path, pages=str(current_page))[0]
        print("first")
        print(df)
        for i in df.index:
            # compare the column with row i
            value = df.loc[i][0]
            print(value)

            if value in index_to_save:
                df.loc[i][0] = index_to_save[value]
            else:
                df.drop(i, inplace=True)

        transposed = df.T
        # delete last row
        transposed.drop(transposed.tail(1).index, inplace=True)

        # modify month axes
        transposed.rename(index={"CONCEPTO": f"datetime"}, inplace=True)

        for column in transposed.columns:
            transposed[column] = transposed[column].apply(remove_char)

        for i in transposed.index:
            if i in converter:
                print("found")
                transposed.rename(index={i: f"{year}-{converter[i]}-01"}, inplace=True)
        print(transposed)

        if year == 2013:
            dataframes[state] = dataframes[state].append(transposed, ignore_index=False)
        else:
            # delete first row
            transposed.drop(transposed.head(1).index, inplace=True)
            dataframes[state] = dataframes[state].append(transposed, ignore_index=False)
        # add to state dataframe
        print(dataframes[state])
        if year == 2016:
            dataframes[state].to_csv(f"{state}.csv", index=True, header=False, sep=";")

    current_page += 1



"""
df = df[0].T
for i in df.index:
    if i in converter:
        df.rename(index={i: f"{converter[i]}"}, inplace=True)

print(df)
"""