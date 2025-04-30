import requests


class Client:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = "https://therapy-bridge-owlbotpierrepon.replit.app/api"
        #self.base_url = "https://1873a6f6-7203-439e-acb8-71ddc9ef832d-00-eock9zltkx6.riker.replit.dev/api"

        self.session = requests.Session()
        self.session.post(f'{self.base_url}/login', json={"username": username, "password": password})
        self.children = self.list_children()

    def list_children(self):
        res = self.session.get(f'{self.base_url}/children')

        if res.status_code == 200:
            res = res.json()
        else:
            raise Exception(f"Error: {res.status_code} - {res.text}")

        children = []
        for child in res:
            children.append(Child(
                client=self,
                name=child['name'],
                age=child['age'],
                start_date=child['therapyStartDate'],
                status=child['status'],
                guardian=child['guardianId'],
                therapist=child['therapistId'],
                id=child['id']
            ))
        return children


class Child:
    def __init__(self, client, name, age, start_date, status, guardian, therapist, id):
        self.client = client

        self.name = name
        self.age = age
        self.start_date = start_date
        self.status = status
        self.guardian = guardian
        self.therapist = therapist
        self.id = id

    def log_emotion(self, emotion, intensity, note='Self Reported During Session'):
        res = self.client.session.post(f'{self.client.base_url}/children/{self.id}/emotions',
                                       json={"childId": self.id, "emotion": emotion, "intensity": intensity,
                                             "note": note})
        print(res.text)


if __name__ == '__main__':
    client = Client('drsmith', 'password')
    child = client.list_children()[0]
    child.log_emotion('Sad', 4, 'Self Reported During Session')
