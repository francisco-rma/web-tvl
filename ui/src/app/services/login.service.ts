import { HttpClient, HttpParams } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { LoginRequest } from "../requests/login.request";

@Injectable({ providedIn: 'root' })
export class LoginService {
    constructor(private http: HttpClient) {
        this.http = http;
    }
    login(request: LoginRequest) {
        const body = new HttpParams()
            .set('username', request.username)
            .set('password', request.password)
            .set('grant_type', 'password');

        return this.http.post(`http://localhost/api/v1/login/access-token`, body);
    }
    login_access_token(request: any) {
        return this.http.post(`http://localhost/api/v1/login/test-token`, request);
    }

    test_token(request: any, email: string) {
        return this.http.post(`http://localhost/api/v1/password-recovery/${email}`, request);
    }

    recover_password(request: any,) {
        return this.http.post(`http://localhost/api/v1/reset-password`, request);
    }

    reset_password(request: any,) {
        return this.http.post(`http://localhost/api/v1/login`, request);
    }

    recover_password_html_content(request: any,) {
        return this.http.post(`http://localhost/api/v1/login`, request);
    }

}