import { Routes } from '@angular/router';
import { UsersComponent } from './users/users.component';
import { TasksComponent } from './tasks/tasks.component';
import { AuthGuard } from './guards/auth.guard';
import { LoginComponent } from './login/login.component';

export const routes: Routes = [
    { path: '', component: LoginComponent },
    { path: 'users', component: UsersComponent, canActivate: [AuthGuard] },
    { path: 'tasks', component: TasksComponent, canActivate: [AuthGuard] },
];
