import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { MenuComponent } from "../menu/menu.component";

@Component({
  selector: 'app-users',
  standalone: true,
  imports: [RouterModule, MenuComponent],
  templateUrl: './users.component.html',
  styleUrl: './users.component.css'
})

export class UsersComponent {

}
