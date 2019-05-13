import json, os

#Problema -> esta a usar ./, portanto cria os ficheiros em qualquer sítio onde seja executado, pode dar problemas ao executar em sitios diferentes e ele nao ler o que já existia
# Decidir o que guardar no following

class MyStorage:

    def __init__(self, username):
        """
        Construtor da classe MyStorage.
        Atributos:
            username : nome de utilizador
        """
        self.username = username
        self.exists_file()

    def exists_file(self):
        """
        Testa se já existe ficheiro para armazenamento do utilizador em questão.
        """
        exists = os.path.isfile('./' + self.username + '.json')
        if not exists:
            print('O ficheiro de armazenamento não existe, temos de criar um novo!')
            self.create_file()
        else:
            print('O ficheiro já existe!')


    def create_file(self):
        """
        Método que cria um ficheiro para armazenamento local, com o formato necessário.
        Devolve um objeto JSON vazio
        """
        data = {}
        data['username'] = self.username
        data['timeline'] = []
        data['following'] = {}
        data['following_timeline'] = []
        nome = self.username + '.json'
        with open(nome, 'w') as outfile:  
            json.dump(data, outfile)
        return data

    def read(self):
        """
        Método que le um ficheiro do armazenamento local.
        Devolve um objeto JSON com o username, a timeline e a lista dos utilizadores que o utilizador atual segue.
        """
        
        data = {}
        try:
            with open(self.username + '.json', 'r') as f:
                data = json.load(f)

        except FileNotFoundError:
            data = self.create_file()
        finally:
            return data

    def write(self, data):

        """
        Método que escreve em disco os dados relativos a um utilizador.
        """

        with open(self.username + '.json', 'w') as outfile:  
            json.dump(data, outfile)


    def write_timeline(self, posts, following, timeline):

        """
        Método que atualiza o ficheiro local de um utilizador. É invocado sempre que o utilizador se desconecta.
        """

        data = self.read()
        data['following_timeline'] = posts
        data['following'] = following
        data['timeline'] = timeline
        
        self.write(data)

    def clear_post(self, username):
        print('PARA FAZER ISTO ...')