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

    def write_my_timeline(self, post):

        """
        Método que adiciona à timeline do utilizador um novo post.
        """
        
        data = self.read()
        data['timeline'].append(post)
        self.write(data)

    def add_following(self, newFollowing, timelineNewFollowing = []):

        """
        Método que adiciona ao campo following um novo utilizador.
        Adiciona uma associação newFollowing -> timelineNewFollowing. 
        """

        data = self.read()
        following = data['following']
        if newFollowing in following:
            print('O utilizador ' + newFollowing + 'já existe no armazenamento local')
            
        else:
            following[newFollowing] = timelineNewFollowing
        self.write(data)


    def write_following_timeline(self, post, username):

        """
        Método que adiciona à timeline local de um utilizador que eu sigo um post.
        """

        data = self.read()
        following = data['following']
        if username in following:
            print('Ja temos a timeline do username: ', username)
            following[username].append(post)
        else:
            print('Temos de criar a timeline do username: ', username)
            lista = [post]
            following[username] = lista
        self.write(data)

    def clear_post(self, username):
        print('PARA FAZER ISTO ...')