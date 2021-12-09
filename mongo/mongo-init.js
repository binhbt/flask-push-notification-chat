db.createUser(
        {
            user: "admin",
            pwd: "adminpwd",
            roles: [
                {
                    role: "readWrite",
                    db: "notify_db"
                }
            ]
        }
);