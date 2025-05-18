import pandas as pd
from statsmodels.formula.api import ols
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.stats.diagnostic import het_breuschpagan
import os

class ANCOVA(object):
    path = r"C:\Users\wisle\Downloads\producao_minas_gerais_2013_2023.xlsx"
    path_graph = r"C:\Artigos Cientificos\Analise_Historica_MG\Files\ANCOVA"

    def __init__(self):
        print('Testando Pressupostos e Teste de Ancova...\n')
        pass

    def control_ancova(self):
        data = self.get_data()
        self.independencia_covariavel_vi(data)
        self.test_linear(data)
        self.slopes(data)
        self.normal_homo(data)
        self.ancova(data)
    
    
    def independencia_covariavel_vi(self, data):
        model_temp = ols("temperatura ~ safra", data=data).fit()
        model_precip = ols("precipitacao ~ safra", data=data).fit()

        print('\n Temperatura \n', sm.stats.anova_lm(model_temp))
        print('\n Precipitação \n', sm.stats.anova_lm(model_precip))
    
    def test_linear(self, data):
        print('\n Gráfico de Linearidade entre covariáveis e variável dependente \n')

        g = sns.lmplot(x="temperatura", y="producao", data=data)
        g.fig.suptitle("Relação entre Temperatura e Produção")
        plt.savefig(os.path.join(self.path_graph, "temperatura_vs_producao.png"))


        g = sns.lmplot(x="precipitacao", y="producao", data=data)
        g.fig.suptitle("Relação entre Precipitação e Produção")
        plt.savefig(os.path.join(self.path_graph, "precipitacao_vs_producao.png"))
    
    def slopes(self, data): 
        model_temp = ols("producao ~ C(grupo_safra) * temperatura", data=data).fit()
        model_precip = ols("producao ~ C(grupo_safra) * precipitacao", data=data).fit()
        
        print('\n ANOVA Tipo III - Temperatura')
        print(sm.stats.anova_lm(model_temp, typ=3))

        print('\n ANOVA Tipo III - Precipitação')
        print(sm.stats.anova_lm(model_precip, typ=3))
    
    def normal_homo(self, data):
        model_temp = ols("producao ~ C(grupo_safra) * temperatura", data=data).fit()
        model_precip = ols("producao ~ C(grupo_safra) * precipitacao", data=data).fit()

        print('\n Temperatura - Shapiro Wilk \n', stats.shapiro(model_temp.resid))
        print('\n Temperatura - Breusch-Pagan \n', het_breuschpagan(model_temp.resid, model_precip.model.exog))

        print('\n Temperatura - Shapiro Wilk \n', stats.shapiro(model_precip.resid))
        print('\n Temperatura - Breusch-Pagan \n', het_breuschpagan(model_precip.resid, model_precip.model.exog))

    def ancova(self, data):
        model_ancova = ols("producao ~ C(grupo_safra) + temperatura + precipitacao", data=data).fit()
        print(sm.stats.anova_lm(model_ancova, typ=2))


    def get_data(self):
        data = pd.read_excel(self.path)
        data.columns = ['safra', 'producao', 'temperatura', 'precipitacao']
        data['safra'] = data['safra'].str[:4].astype(int)
        data['grupo_safra'] = data['safra'].apply(self.agrupar_safras)

        print('\n', data, '\n')

        return data
    
    def agrupar_safras(self, safra):
        if safra <= 2016:
            return '2013-2016'
        elif safra <= 2020:
            return '2017-2020'
        else:
            return '2021-2023'

def main():
    ancova = ANCOVA()
    ancova.control_ancova()

if __name__ == '__main__':
    main()