import re

class AnalisadorLexico:
    def __init__(self):
        # Definição das Regras com Expressões Regulares (Item 1.3 da sua pesquisa)
        self.regras = [
            ('COMENTARIO', r'//.*|/\*[\s\S]*?\*/'), 
            ('PALAVRA_RESERVADA', r'\b(int|float|string|if|else|while|print|return|void)\b'),
            ('IDENTIFICADOR', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('NUMERO', r'\d+(\.\d+)?'),
            ('OPERADOR', r'[+\-*/=<>!]+'),
            ('DELIMITADOR', r'[(){}\[\];,]'),
            ('ESPACO', r'\s+'), 
            ('ERRO', r'.'),     
        ]
        
        regex_parts = [f'(?P<{nome}>{padrao})' for nome, padrao in self.regras]
        self.regex_master = re.compile('|'.join(regex_parts))

    def analisar(self, codigo_fonte):
        tokens = []
        tabela_simbolos = {}
        linha_atual = 1
        
        for match in self.regex_master.finditer(codigo_fonte):
            tipo = match.lastgroup
            lexema = match.group(tipo)
            
            # 1. Eliminação de espaços e comentários (Item 2 do PDF)
            if tipo == 'ESPACO' or tipo == 'COMENTARIO':
                linha_atual += lexema.count('\n')
                continue 
            
            if tipo != 'ERRO':
                tokens.append((tipo, lexema, linha_atual))
                
                # 2. Gestão da Tabela de Símbolos (Conforme sua pesquisa)
                if tipo == 'IDENTIFICADOR':
                    # Lógica para descobrir o tipo: checa se o token anterior era uma palavra reservada
                    tipo_declarado = "desconhecido"
                    if len(tokens) > 1:
                        ultimo_token = tokens[-2]
                        if ultimo_token[0] == 'PALAVRA_RESERVADA':
                            tipo_declarado = ultimo_token[1]

                    if lexema not in tabela_simbolos:
                        # Gera um endereço hexadecimal fictício para a localização (Item 1.4 da pesquisa)
                        endereco_memoria = f"0x{hex(abs(hash(lexema)))[2:6].upper()}"
                        
                        tabela_simbolos[lexema] = {
                            "tipo": tipo_declarado,
                            "escopo": "global",
                            "endereco": endereco_memoria
                        }
            else:
                tokens.append(('ERRO_LEXICO', lexema, linha_atual))
                
            linha_atual += lexema.count('\n')
            
        return tokens, tabela_simbolos