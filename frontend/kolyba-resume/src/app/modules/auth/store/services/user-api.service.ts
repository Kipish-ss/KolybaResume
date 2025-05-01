import * as authActions from '../actions/auth.actions';

import { BehaviorSubject, Observable, catchError, from, map, of, tap } from 'rxjs';

import { Action } from '@ngrx/store';
import { HttpInternalService } from '@core/services/http-internal.service';
import { Injectable } from '@angular/core';
import { NewUser } from '../../models/new-user';
import { NotificationService } from '@core/services/notification.service';
import { UpdateUser } from '../../models/update-user';
import { User } from '../../models/user';

@Injectable({
    providedIn: 'root',
})
export class UserApiService {
    public routePrefix = '/user';

    constructor(private httpService: HttpInternalService, private notificationService: NotificationService) {}

    public getCurrentUser(): Observable<Action> {
        return this.httpService.getRequest<User>(this.routePrefix).pipe(
            map((user) => authActions.setCurrentUser({ user })),
            catchError(() => of(authActions.loadCurrentFailure({ error: new Error() }))),
        );
    }

    public createUser(newUser: NewUser): Observable<Action> {
        return this.httpService.postRequest<User>(this.routePrefix, newUser).pipe(
            map((user) => authActions.createUseruccess({ user })),
            catchError(() => of(authActions.createUserFailure({ error: new Error() }))),
        );
    }

    public uploadResume(file: File): Observable<Action> {
        return this.httpService.postRequest<void>(`${this.routePrefix}/resume`, file).pipe(
            map(() => authActions.uploadResumeSuccess()),
            catchError(() => of(authActions.uploadResumeFailure({ error: new Error() }))),
        );
    }

    public checkExistingEmail(email: string): Observable<boolean> {
        const emailEncoded = encodeURIComponent(email);

        return this.httpService.getRequest<boolean>(`${this.routePrefix}/check-email?email=${emailEncoded}`).pipe(
            tap({
                error: () =>
                    this.notificationService.showErrorMessage('Something went wrong. Failed to verify email exists.'),
            }),
        );
    }
}
