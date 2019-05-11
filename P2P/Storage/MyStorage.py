import json, os

class MyStorage:

    def __init__(self, username):
        self.username = username
        self.exists_file()

    def exists_file(self):
        '''
        Testa se o ficheiro já está criado


        '''
        exists = os.path.isfile('./' + self.username + '.json')
        if not exists:
            print('O ficheiro não existe, temos de criar um novo')
            self.create_file()
        else:
            print('O ficheiro já existe!')


    def create_file(self):
        data = {}
        data['username'] = self.username
        data['timeline'] = []
        data['following'] = {}
        nome = self.username + '.json'
        with open(nome, 'w') as outfile:  
            json.dump(data, outfile)
        return data

    def read(self):
        data = {}
        try:
            with open(self.username + '.json', 'r') as f:
                data = json.load(f)

        except FileNotFoundError:
            data = self.create_file()
        finally:
            return data

    def write(self, data):
        with open(self.username + '.json', 'w') as outfile:  
            json.dump(data, outfile)

    def write_my_timeline(self, post):
        data = self.read()
        data['timeline'].append(post)
        self.write(data)

    def write_following_timeline(self, post, username):
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