from Tasks.Setup import setup
from Tasks.SignIn import signin

def main():
    driver = setup()
    signin(driver)



if __name__ == "__main__":
    main()