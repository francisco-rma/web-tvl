export class LoginRequest {
    constructor(username: string, password: string,) {
        this.username = username;
        this.password = password;
    }

    public username: string;
    public password: string;
    public grant_type: string = 'password';
}