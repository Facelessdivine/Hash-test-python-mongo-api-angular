import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';



@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {
  username: string;
  password: string;
  c_password: string;


  clear1(){
    this.user.username = ''
  }
  clear2(){
    this.user.password = ''
    this.user.c_password = ''
  }
  user = {
    username: '',
    password: '',
    c_password: ''
  }
  
  response = '';
  show= false;
  show2 = false;

  constructor(private authService: AuthService,
  private router: Router
  ) { 
    if (authService.getToken() != null){
      this.router.navigate(['/private-tasks']);
    } 
  }

  ngOnInit() {

  }
  signUp(){
    this.authService.signUp(this.user)
    .subscribe( res => {
      if(res.alert){
      this.response= res.alert
      this.show = true
      if(res.alert == 'Passwords do not match'){
        this.clear2()
      }
      else{
        this.clear1()
      }
      } else {
        localStorage.setItem('token', res.token);
        this.router.navigate(['/private-tasks']);
      }
    })
  }

}
