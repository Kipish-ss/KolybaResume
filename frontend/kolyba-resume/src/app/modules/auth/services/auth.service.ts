import { Auth, User, UserCredential, createUserWithEmailAndPassword, signOut as firebaseSignOut, onAuthStateChanged, sendPasswordResetEmail, signInWithEmailAndPassword } from '@angular/fire/auth';
import { Observable, concatMap, defer, first, from, of } from 'rxjs';
import { accessTokenLocalStorage, emailVerifiedLocalStorage, userLocalStorage } from '@core/constants/local-storage.constants';
import { map, take, tap } from 'rxjs/operators';

import { Injectable } from '@angular/core';
import { NotificationService } from '../../core/services/notification.service';
import { UserApiService } from '../store/services/user-api.service';
import { sendEmailVerification } from '@angular/fire/auth';

@Injectable({
    providedIn: 'root',
})
export class AuthService {
    constructor(
        private auth: Auth,
        private userService: UserApiService,
        private notificationService: NotificationService,
    ) {
    }

    public signUp(email: string, password: string): Observable<UserCredential> {
        return defer(() => createUserWithEmailAndPassword(this.auth, email, password)).pipe(
            first(),
            tap({
                next: () => this.sendEmailVerification().subscribe(),
                error: (e) => this.notificationService.showErrorMessage(e.message),
            }),
        );
    }

    public signIn(email: string, password: string): Observable<UserCredential> {
        return defer(() => signInWithEmailAndPassword(this.auth, email, password)).pipe(
            first(),
            tap({
                next: (userCredential) => {
                    if (userCredential.user) {
                        from(userCredential.user.getIdToken()).pipe(take(1))
                            .subscribe(token => localStorage.setItem(accessTokenLocalStorage, token));

                        if (!userCredential.user.emailVerified) {
                            const emailNotVerified = new Error('Email is not verified');
                            emailNotVerified.name = 'Email-not-verified';
                            throw emailNotVerified;
                        }
                    }
                },
                error: (e) => this.notificationService.showErrorMessage(e.message),
            }),
        );
    }

    public resetPassword(email: string): Observable<void> {
        return defer(() => sendPasswordResetEmail(this.auth, email)).pipe(
            first(),
            tap({
                error: (e) => this.notificationService.showErrorMessage(e.message),
            }),
        );
    }

    public signOut(): Observable<void> {
        return defer(() => firebaseSignOut(this.auth)).pipe(
            first(),
            tap({
                next: () => {
                    localStorage.removeItem(userLocalStorage);
                    localStorage.removeItem(emailVerifiedLocalStorage);
                    localStorage.removeItem(accessTokenLocalStorage);
                },
                error: (e) => this.notificationService.showErrorMessage(e.message),
            }),
        );
    }

    public isLoggedIn(): boolean {
        return JSON.parse(localStorage.getItem(emailVerifiedLocalStorage)!) as boolean;
    }

    public refreshToken(): Observable<void> {
        return defer(() => of(this.auth.currentUser)).pipe(
            first((u) => !!u),
            concatMap((u) => this.setUserAccessToken(u!)),
        );
    }

    public getAccessToken() {
        return localStorage.getItem(accessTokenLocalStorage);
    }

    private sendEmailVerification(): Observable<void> {
        return defer(async () => {
            const user = this.auth.currentUser;
            if (user) {
                await sendEmailVerification(user);
            }
        }).pipe(
            first(),
            tap({
                error: (e) => this.notificationService.showErrorMessage(e.message),
            }),
        );
    }

    public checkEmail(email: string): Observable<boolean> {
        return this.userService.checkExistingEmail(email).pipe(map((res) => res));
    }

    private async setUserAccessToken(user: User) {
        const token = await user.getIdToken();
        localStorage.setItem(accessTokenLocalStorage, token);
    }
}
