import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormControl, Validators } from '@angular/forms';
import { LoginRequest } from '../requests/login.request';
import { ReactiveFormsModule } from '@angular/forms';
import { LoginService } from '../services/login.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent implements OnInit {
  constructor(
    private formBuilder: FormBuilder,
    private loginService: LoginService,
  ) { }
  public loginForm: FormGroup = new FormGroup({});

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  submit() {
    console.log(this.loginForm.value);
    let request = new LoginRequest(this.loginForm.value.username, this.loginForm.value.password);
    console.log(request);
    this.loginService.login(request).subscribe((response) => {
      console.log(response);
    });
  }
}
