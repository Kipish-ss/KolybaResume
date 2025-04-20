import { Observable, finalize, switchMap, tap } from 'rxjs';

import { AuthService } from './auth.service';
import { Injectable } from '@angular/core';
import { NotificationService } from '@core/services/notification.service';
import { Router } from '@angular/router';
import { SpinnerService } from '@core/services/spinner.service';
import { User } from '../models/user';
import { UserApiService } from '../store/services/user-api.service';
import { UserCredential } from '@angular/fire/auth';

@Injectable({
    providedIn: 'root',
})
export class AuthFormService {
    constructor(
        private authService: AuthService,
        private spinnerService: SpinnerService,
        private userService: UserApiService,
        private notificationService: NotificationService,
        private router: Router,
        // eslint-disable-next-line no-empty-function
    ) {}

    public signIn(email: string, password: string): Observable<User> {
        return this.authenticate(this.authService.signIn(email, password)).pipe(
            tap({
                next: () => this.notificationService.showSuccessMessage('Authentication successful'),
                error: () =>
                    this.notificationService.showErrorMessage("You've entered wrong password! Please try again or reset your password."),
            }),
        );
    }

    public signUp(email: string, password: string, userName: string): Observable<User> {
        return this.authenticate(this.authService.signUp(email, password), userName).pipe(
            tap({ next: () => this.notificationService.showInfoMessage('Verification email has been sent') }),
        );
    }

    public resetPassword(email: string): Observable<void> {
        return this.authService
            .resetPassword(email).pipe(
                tap(() =>
                    this.notificationService.showSuccessMessage(`Link for resetting password was send to this ${email} email`)),
            );
    }

    private authenticate(authMethod: Observable<UserCredential>, userName?: string): Observable<User> {
        this.spinnerService.show();

        return authMethod.pipe(
            finalize(() => this.spinnerService.hide()),
            switchMap((userCredential) => this.createUser(userCredential, userName)),
        );
    }

    private createUser(resp: UserCredential, userName: string = 'UserName'): Observable<User> {
        return this.userService
            .createUser({
                userName: resp.user?.displayName ?? userName,
                email: resp.user?.email ?? '',
                image: resp.user?.photoURL ?? undefined,
            })
            .pipe(
                tap(() => {
                    this.router.navigateByUrl('');
                }),
            );
    }
}
