# -*- coding: utf-8 -*-
import xmlrpclib
import sys
import os
import time

class connect_odoo(object):

    def __init__(self, dic_info):
        self.dic_info = dic_info
        self.uid = self.get_uid_user()
        self.id_last_client = False
        self.model = self.init_call_method()
        self.menu()

    def menu(self):
        print "====== ODOO TEST ======"
        print "1 - Inserir cliente"
        print "2 - Atualizar RG cliente recém cadastrado pelo programa"
        print "3 - Quantidade total de clientes na base de dados"
        print "0 - Sair"
        option = raw_input("Opção: ")
        
        if option == "0":
            sys.exit()

        elif option == "1":
            print ">>>> 1 - Inserir cliente"
            nome = raw_input("Nome: ")
            email = raw_input("E-mail: ")
            telefone = raw_input("Telefone: ")
            cep = raw_input("CEP: ")
            id_client = self.inserir_cliente(nome, email, telefone, cep)
        elif option == "2":
            print ">>>> 2 - Atualizar RG cliente recém cadastrado pelo programa"
            if self.id_last_client is False:
                print "Depois que o programa iniciou nenhum cliente foi cadastrado!"
                self.waiting_message_return()
            else:          
                self.atualizar_cliente_rg()
            
        elif option == "3":
            print ">>>> 3 - Quantidade total de clientes na base de dados"
            self.qtd_total_clientes()

        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.menu()
            
        if option != "0":
            os.system('cls' if os.name == 'nt' else 'clear')
            self.menu()

    def get_uid_user(self):
        """ make authentication """
        info = xmlrpclib.ServerProxy(self.dic_info["url"] + '/xmlrpc/2/common')
        uid_user = info.authenticate(self.dic_info["db"], self.dic_info["username"], self.dic_info["password"], {})
        return uid_user

    def info_buscando_cliente(self, id_client):
        model_name = "res.partner"
        info = self.model.execute_kw(self.dic_info["db"], self.uid, self.dic_info["password"], model_name, "search_read",
            [[["id", "=", id_client]]], {"fields": ["name", "email", "phone", "zip", "rg_fisica"], "limit": 1})
        return info

    def init_call_method(self):
        """ call method """
        model = xmlrpclib.ServerProxy(self.dic_info["url"] + '/xmlrpc/2/object')
        return model

    def inserir_cliente(self, nome, email, telefone, cep):
        # 1 - Inserir um cliente no Odoo via api, com os seus dados (Nome, email, telefone, cep)
        id_client, model_name = False, "res.partner"
        dic = {"name": nome, "email": email, "phone": telefone, "zip": cep}
        try:
            id_client = self.model.execute_kw(self.dic_info["db"], self.uid, self.dic_info["password"], model_name, "create", [dic])
            if id_client != False:
                self.id_last_client = id_client
                print "Cliente cadastrado com sucesso!"
        except:
            print "Não foi possível cadastrar cliente!"
        
        self.waiting_message_return()
        return id_client

    def atualizar_cliente_rg(self):
        # 2 - Atualizar cadastro do cliente recém criado para adicionar o RG do mesmo.
        rg_number = raw_input("Digite RG: ")
        model_name = "res.partner"
        dic = {"rg_fisica": rg_number}
        try:
            self.model.execute_kw(self.dic_info["db"], self.uid, self.dic_info["password"], model_name, "write", [[self.id_last_client], dic])
            info_client = self.info_buscando_cliente(self.id_last_client)
            if info_client[0]["rg_fisica"].__contains__(rg_number):
                print "Cadastro atualizado com sucesso!"
        except:
            print "Não foi possível atualizar cadastro do cliente!"
        
        self.waiting_message_return()

    def qtd_total_clientes(self):
        # 3 - Realizar uma consulta para saber quantos *clientes existem na base de dados.
        qtd_clientes = self.model.execute_kw(self.dic_info["db"], self.uid, self.dic_info["password"], "res.partner", "search_count", [[["customer", "=", True]]])
        print "Qtd. Clientes: " + str(qtd_clientes)
        self.waiting_message_return()

    def waiting_message_return(self):
        print "clique em [enter] para retornar ao menu principal ..."
        raw_input()


dic_info = {
    "url": "https://enterprise.trustcode.com.br",
    "db": "enterprise",
    "username": "teste123",
    "password": "123",
}

# connection
conn = connect_odoo(dic_info)


