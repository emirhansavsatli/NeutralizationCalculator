# NeutralizationCalculator
Features

- The program allows the user to enter the compound's formula in capital letters.
- It retrieves the features of the compound from a database file (`data.txt`), including boiling point, name, molecular weight, and other features.
- The user can choose a neutralization formula that contains the entered compound from a list of available formulas in the `formula.txt` file.
- The program extracts the coefficients and other compounds from the chosen formula.
- It calculates the amount of the entered compound, the number of moles, and the number of moles for each product compound.
- A PDF report is generated using the `reportlab` library, displaying the formula, coefficients, amount, number of moles, and number of moles for each product compound.
- The PDF report is saved as `<compound_name>_report.pdf` and opened using the default PDF viewer.
- The chosen formula and its coefficients are saved in the `formulaK.txt` file for future reference.
