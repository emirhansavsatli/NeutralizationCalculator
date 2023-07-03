import sys
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def kaydet_formul(formula, coefficients):
    with open("formulaK.txt", "a") as dosya:
        dosya.write(f'"{formula}": {coefficients},\n')


def create_pdf(chosen_formula, coefficients, amount_onhand, mole_numbers, mol_number):
    name_file = firstname + "_rapor.pdf"
    pdf = canvas.Canvas(name_file, pagesize=letter)
    pdf.setTitle(chosen_formula)

    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(50, 750, "Neutralization Report")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(70, 700, f"Formula: {chosen_formula}")
    pdf.drawString(70, 680, f"Coefficients: {coefficients}")
    pdf.drawString(150, 660, f"{firstname} Amount: {amount_onhand} gram")
    pdf.drawString(150, 640, f"{firstname} Number of Mole: {mol_number} mol")

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, 600, "Mole Number of Products:")

    pdf.setFont("Helvetica", 12)
    y = 580
    for compound, mol_number in mole_numbers.items():
        pdf.drawString(150, y, f"{compound}: {mol_number}")
        y -= 20

    pdf.save()
    os.startfile(name_file)

    print(f"Report generated as PDF file: {name_file}")


print("Hello, welcome to the neutralization calculator.")
firstname = input("Please enter the compound using large characters: ")

class Features:
    def __init__(self, heat, name, molecular_weight, features):
        self.heat = heat
        self.name = name
        self.molecular_weight = molecular_weight
        self.features = features

    def print_features(self):
        print("Boiling point:", self.heat)
        print("Name:", self.name)
        print("Molecular Weight:", self.molecular_weight)
        print("Feature:", self.features)

material_dict = {}

with open("data.txt", "r") as dosya:
    for satır in dosya:
        data = satır.strip("()\n").split(", ")
        formula = data[0]
        heat = float(data[1])
        name = data[2]
        molecular_weight = float(data[3])
        features = data[4]
        material_dict[formula] = Features(heat, name, molecular_weight, features)

if firstname in material_dict:
    print(firstname.upper(), "Features:")
    material_dict[firstname].print_features()
    print()

    print("Formulas containing:", firstname)
    with open("formula.txt", "r") as dosya:
        formulas = [satır.strip() for satır in dosya if firstname in satır]

    if formulas:
        for i, formula in enumerate(formulas, start=1):
            print(f"{i}. {formula}")

        chose = int(input("Choose one of the formulas above: "))
        if chose > 0 and chose <= len(formulas):
            chosen_formula = formulas[chose - 1]

            print("Chosen Formula:", chosen_formula)
            coefficients = {}
            formula_parts = chosen_formula.split("=")
            left_materials = formula_parts[0].strip().split("+")
            right_materials = formula_parts[1].strip().split("+")
            for material in left_materials:
                match = re.match(r'(\d+)?(\w+)', material.strip())
                if match:
                    katsayi = int(match.group(1)) if match.group(1) else 1
                    bileşik_adı = match.group(2)
                    coefficients[bileşik_adı] = -katsayi
            for material in right_materials:
                match = re.match(r'(\d+)?(\w+)', material.strip())
                if match:
                    katsayi = int(match.group(1)) if match.group(1) else 1
                    bileşik_adı = match.group(2)
                    coefficients[bileşik_adı] = katsayi
            print("Coefficients:", coefficients)
            kaydet_formul(chosen_formula, coefficients)

            amount_onhand = float(input(f"Enter the amount: {firstname.upper()}  "))

            mole_numbers = {}
            mole_number = amount_onhand / material_dict[firstname].molecular_weight
            for compound, katsayi in coefficients.items():
                if compound == firstname:
                    continue
                mmol_sayisi_bileşik = mole_number * abs(katsayi)
                mole_numbers[compound] = mmol_sayisi_bileşik

            print(f"{firstname.upper()} mole number:", mole_number)
            print("Mole Number of Products:")
            for compound, mole_number in mole_numbers.items():
                print(compound, ":", mole_number)

            create_pdf(chosen_formula, coefficients, amount_onhand, mole_numbers, mole_number)
            name_file = firstname + "_raport.pdf"
            print(f"Report generated as PDF file: {name_file}")

        else:
            print("You have made an invalid choice.")
            sys.exit()
    else:
        print("The formula was not found.")
else:
    print("The compound entered was not found in the database.")
    sys.exit()
