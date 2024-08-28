db =db.getSiblingDB('BushtreeDB')

db.createUser(
    {
      user: "Modestra",
      pwd: "Terrarik22",
      roles: [
        {
          role: "readWrite",
          db: "BushtreeDB"
        }
      ]
    }
  );