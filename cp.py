#Importando as bibliotecas necessárias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

 # Carregar o CSV e ajustar os valores numéricos
df = pd.read_csv('ipc_brasil.csv', delimiter=",")

# Substituir vírgulas por pontos nos valores numéricos e converter para float
df['Geral'] = df['Geral'].str.replace(',', '.').astype(float)

# Verificar se a coluna 'Data' existe e convertê-la para datetime
if 'Data' in df.columns:
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce') # Converte 'Data' para datetime
else: # Se não houver coluna 'Data', criar a partir de 'Ano' e possivelmente de um campo 'Mês', se existir
    df['Data'] = pd.to_datetime(df['Ano'].astype(str), format='%Y') # Converte o ano em uma coluna de data

# Filtrar o intervalo de janeiro de 2023 até agosto de 2024
filtro = (df['Data'] >= '2023-01-01') & (df['Data'] <= '2024-08-31')

#Calcular a média e o desvio padrão das variações no período filtrado
media_geral_periodo = df[filtro]['Geral'].mean()
desvio_geral_periodo = df[filtro]['Geral'].std()

#Exibir os resultados
print(f"Média Geral (jan/2023 - ago/2024): {media_geral_periodo}")
print(f"Desvio Padrão Geral (jan/2023 - ago/2024): {desvio_geral_periodo}")

#Gerar simulações de Monte Carlo para prever os próximos 4 meses (até dezembro de 2024)

#Utilizar a média e desvio padrão calculados para o período de jan/2023 a ago/2024
simulacoes = np.random.normal(media_geral_periodo, desvio_geral_periodo, 1000 * 4) # 4 meses de simulações

#Selecionar as simulações para setembro, outubro, novembro e dezembro de 2024
simulacoes_set_2024 = simulacoes[0:1000] # Setembro de 2024
simulacoes_out_2024 = simulacoes[1000:2000] # Outubro de 2024
simulacoes_nov_2024 = simulacoes[2000:3000] # Novembro de 2024
simulacoes_dez_2024 = simulacoes[3000:4000] # Dezembro de 2024

#Aplicar o ajuste de 0,17% às simulações de setembro com base na projeção do economista Fabio Romão
ajuste_set_2024 = 0.17 # Projeção de alta de 0,17%
simulacoes_set_2024_ajustadas = simulacoes_set_2024 + ajuste_set_2024

#Calcular a média das previsões para os meses de setembro a dezembro de 2024
media_previsoes_set_2024 = np.mean(simulacoes_set_2024_ajustadas)
media_previsoes_out_2024 = np.mean(simulacoes_out_2024)
media_previsoes_nov_2024 = np.mean(simulacoes_nov_2024)
media_previsoes_dez_2024 = np.mean(simulacoes_dez_2024)

#Exibir as médias das previsões para cada mês
print(f"Média das previsões para Setembro 2024 ajustada (variação %):{media_previsoes_set_2024:.4f}")
print(f"Média das previsões para Outubro 2024 (variação %):{media_previsoes_out_2024:.4f}")
print(f"Média das previsões para Novembro 2024 (variação %):{media_previsoes_nov_2024:.4f}")
print(f"Média das previsões para Dezembro 2024 (variação %):{media_previsoes_dez_2024:.4f}")

#Exibir as primeiras 10 simulações para cada mês
print(f"Previsões simuladas para Setembro 2024 (variações %):\n{simulacoes_set_2024_ajustadas[:10]}\n")
print(f"Previsões simuladas para Outubro 2024 (variações %):\n{simulacoes_out_2024[:10]}\n")
print(f"Previsões simuladas para Novembro 2024 (variações %):\n{simulacoes_nov_2024[:10]}\n")
print(f"Previsões simuladas para Dezembro 2024 (variações %):\n{simulacoes_dez_2024[:10]}\n")

# Definir os meses de setembro a dezembro de 2024
meses = ['Setembro', 'Outubro', 'Novembro', 'Dezembro']

# Usar as médias previstas para esses meses
previsoes = [media_previsoes_set_2024, media_previsoes_out_2024,
            media_previsoes_nov_2024, media_previsoes_dez_2024]

# Plotar o gráfico
plt.figure(figsize=(10, 6))
plt.plot(meses, previsoes, marker='o', color='b', label='Previsão de Variação(%)')

# Adicionar título e rótulos
plt.title('Previsão de Variação do IPC - Setembro a Dezembro de 2024',fontsize=14)
plt.xlabel('Meses de 2024', fontsize=12)
plt.ylabel('Variação (%)', fontsize=12)

# Adicionar legenda
plt.legend()

# Exibir grid e gráfico
plt.grid(True)
plt.show()

# Função para calcular o erro MAPE (Mean Absolute Percentage Error)
def mape(real, previsto):
    return np.mean(np.abs((real - previsto) / real)) * 100

# Valores reais de 2024 (variações %)
real_2024 = df[df['Ano'] == 2024]['Geral']

# Usar a simulação da média como previsão para os meses de 2024 já disponíveis
previsoes_2024 = simulacoes[:len(real_2024)]

# Calcular o erro MAPE até o momento (até o mês com valores reais)
erro_mape = mape(real_2024, previsoes_2024)
print(f"Erro MAPE até agora para 2024: {erro_mape}%")
