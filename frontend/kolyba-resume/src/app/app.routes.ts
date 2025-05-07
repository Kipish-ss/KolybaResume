import { AuthGuard } from '@core/guards/auth.guard';
import { Routes } from '@angular/router';

export const routes: Routes = [
    {
        path: 'auth',
        loadChildren: () => import('./modules/auth/auth.module').then((m) => m.AuthModule),
    },
    {
        path: '',
        loadChildren: () => import('./modules/vacancies/resume.module').then((m) => m.ResumeModule),
        canActivate: [AuthGuard]
    },
];
