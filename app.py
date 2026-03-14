import pandas as pd 

def corrigir_dados():
    # Carregar os dados do arquivo CSV
    df = pd.read_csv('dados.csv')
    for index, row in df.iterrows():
        empresa_origem = row['empresa_origem']
        cliente_destino = row['cliente_destino']
        id = row['id_envio']
        if index > 20:
            break
        
        if empresa_origem == '-' or pd.isna(empresa_origem):
            print ('Empresa de origem inválida:',empresa_origem, id)
        if cliente_destino == '-' or pd.isna(cliente_destino):
            print ('Cliente destino inválido:',cliente_destino, id) 



if __name__ == "__main__":
    corrigir_dados() 


