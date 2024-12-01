import fitz

'''
GeneratePDF e uma funcao que customiza um PDF com os dados recebidos,
tendo como ideia principal modificar capas de documentos PDF. (principalmente para trabalhos escolares/acadêmicos)
Para gerar uma nova capa e necessario os seguintes dados:
course - Nome do curso
matter - Nome da disciplina
name - Nome do aluno
aluno_id - Matrícula do aluno
city - Cidade
@params: course, matter, name, id, city
Com esses dados, e obviamente a capa modificada, para encontrar os campos corretos a serem substituídos,
o programa irá trocar os campos com os valores recebidos, entao e gerado um novo PDF com a capa modificada.
'''
# #FUTURE-TODO: Implementar um custom field para o usuario escolher os campos a serem modificados

class GeneratePDF:
    def __init__(self, path):
        self.doc = fitz.open(path)


    def open_page(self, course, matter, name, id, city):
        field_dict = {
            "curso": course,
            "matéria": matter,
            "nome": "",
            "aluno_id": "",
            "cidade": city,
            "+" : ""
        }

        for page_num in range(len(self.doc)):
            page = self.doc.load_page(page_num)
            
            text = page.get_text("text").lower()
            
            if "+" in text:
                areas = page.search_for("+")
                for area in areas:
                    page.draw_rect(area, color=(1, 1, 1), fill=(1, 1, 1)) 
                    name_area = page.search_for("nome")
                    id_area = page.search_for("aluno_id")
                    
                    if name_area and id_area:
                        name_pos = name_area[0][:2]
                        id_pos = id_area[0][:2]
                        
                        page.insert_text(name_pos, name, fontsize=12, color=(0, 0, 0))
                        page.insert_text((id_pos[0] + 50, id_pos[1]), id, fontsize=12, color=(0, 0, 0))

            for field, value in field_dict.items():
                if field in text:
                    areas = page.search_for(field)
                    for area in areas:
                        page.draw_rect(area, color=(1, 1, 1), fill=(1, 1, 1))
                        pos_x, pos_y = area[:2]
                        
                        font_size = 14 if field != "matéria" else 16
                        vertical_offset = font_size * 0.8

                        page.insert_text((pos_x, pos_y + vertical_offset), value, fontsize=font_size, color=(0, 0, 0), fontname="times-bold")



        self.doc.save("capa_modificada.pdf")
        print("PDF modificado com sucesso!")
