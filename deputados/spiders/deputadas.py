import scrapy
from scrapy.selector import Selector


class DeputadasSpider(scrapy.Spider):
    name = "deputadas"

    def start_requests(self):
        urls = []

        with open('../lista_deputadas.txt', 'r') as deputadas_f:
            lines = deputadas_f.readlines()

            for l in lines:
                urls.append(l)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        nome = response.css('#nomedeputado::text').get()
        presencas = response.css('dd.list-table__definition-description::text').getall()

        informacoes = response.css('ul.informacoes-deputado').get()
        data_nasc = Selector(text=informacoes).xpath('//li/text()').getall()[4]

        gasto_par_info = response.css('#percentualgastocotaparlamentar').get()
        gasto_par = Selector(text=gasto_par_info).xpath('//tbody/tr/td/text()').getall()[1]

        gasto_mensal_par = response.css('#gastomensalcotaparlamentar').get()
        gasto_mensal_par = Selector(text=gasto_mensal_par).xpath('//tbody/tr').getall()

        todos_meses_par = []
        for mes in gasto_mensal_par:
            gasto_mes = Selector(text=mes).xpath('//tr/td/text()').getall()[1]
            todos_meses_par.append(float(gasto_mes.replace('.', '').replace(',', '.')))

        gasto_gab_info = response.css('#percentualgastoverbagabinete').get()
        gasto_gab = Selector(text=gasto_gab_info).xpath('//tbody/tr/td/text()').getall()[1]

        gasto_mensal_gab = response.css('#gastomensalverbagabinete').get()
        gasto_mensal_gab = Selector(text=gasto_mensal_gab).xpath('//tbody/tr').getall()

        todos_meses_gab = []
        for mes in gasto_mensal_gab:
            gasto_mes_gab = Selector(text=mes).xpath('//tr/td/text()').getall()[1]
            todos_meses_gab.append(float(gasto_mes_gab.replace('.', '').replace(',', '.')))

        salario_div = response.css('div.beneficio').getall()[1]
        salario = Selector(text=salario_div).xpath('//a/text()').getall()[1]
        salario = salario.split()[1]
        salario = salario.replace('.', '').replace(',', '.')


        dict_dep = {
            'nome': nome,
            'genero': 'F',
            'presencas_plenario': int(presencas[0].strip().split()[0]),
            'ausencia_justificada_plenario': int(presencas[1].strip().split()[0]),
            'ausencia_plenario': int(presencas[2].strip().split()[0]),
            'presenca_comissao': int(presencas[3].strip().split()[0]),
            'ausencia_justificada_comissao': int(presencas[4].strip().split()[0]),
            'ausencia_comissao': int(presencas[5].strip().split()[0]),
            'data_nascimento': data_nasc.strip(),
            'gasto_total_par': float(gasto_par.replace('.', '').replace(',', '.')),
            'gasto_jan_par': todos_meses_par[0],
            'gasto_fev_par': todos_meses_par[1],
            'gasto_mar_par': todos_meses_par[2],
            'gasto_abr_par': todos_meses_par[3],
            'gasto_mai_par': todos_meses_par[4],
            'gasto_jun_par': todos_meses_par[5],
            'gasto_jul_par': todos_meses_par[6],
            'gasto_ago_par': todos_meses_par[7],
            'gasto_set_par': todos_meses_par[8],
            'gasto_out_par': todos_meses_par[9],
            'gasto_nov_par': todos_meses_par[10],
            'gasto_total_gab': float(gasto_gab.replace('.', '').replace(',', '.')),
            'gasto_jan_gab': todos_meses_gab[0],
            'gasto_fev_gab': todos_meses_gab[1],
            'gasto_mar_gab': todos_meses_gab[2],
            'gasto_abr_gab': todos_meses_gab[3],
            'gasto_mai_gab': todos_meses_gab[4],
            'gasto_jun_gab': todos_meses_gab[5],
            'gasto_jul_gab': todos_meses_gab[6],
            'gasto_ago_gab': todos_meses_gab[7],
            'gasto_set_gab': todos_meses_gab[8],
            'gasto_out_gab': todos_meses_gab[9],
            'salario_bruto': float(salario)
            

        }

        yield dict_dep
