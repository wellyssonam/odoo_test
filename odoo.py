# -*- coding: utf-8 -*-
import xmlrpclib
import sys
import os
import time

class connect_odoo(object):

    def __init__(self, dic_info):
        self.dic_info = dic_info
        self.uid = self.get_uid_user()
        self.model = self.init_call_method()
        self.menu()

    def menu(self):
        print "====== ODOO TEST ======"
        print "1 - Inserir cliente"
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
                print "Cliente cadastrado com sucesso!"
        except:
            print "Não foi possível cadastrar cliente!"
        
        print "em segundos você retornará ao menu principal ....."
        time.sleep(4)
        return id_client



dic_info = {
    "url": "https://enterprise.trustcode.com.br",
    "db": "enterprise",
    "username": "teste123",
    "password": "123",
}

# connection
conn = connect_odoo(dic_info)


