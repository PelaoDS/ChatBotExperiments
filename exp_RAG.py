from langchain_community.document_loaders.csv_loader import CSVLoader

list_field_names = ['index','marca','modelo','version','precio','gasolina','anio','kms','potencia','puertas','cambios','color']
loader = CSVLoader(file_path='autos_clean.csv', 
                   csv_args={'fieldnames': list_field_names})
data = loader.load()
del data[0]
# print(data)
print(type(data), len(data))
# print(data[0])
# print(data[1])
# print(data[2])