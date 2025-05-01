import * as vacanciesActions from '../actions/vacancies.actions';

import { Actions, createEffect, ofType } from '@ngrx/effects';
import { accessTokenLocalStorage, emailVerifiedLocalStorage, userLocalStorage } from '@core/constants/local-storage.constants';
import { catchError, filter, from, map, mergeMap, of, switchMap, tap } from 'rxjs';

import { Injectable } from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import { NotificationService } from '@core/services/notification.service';
import { Router } from '@angular/router';
import { SpinnerService } from '@core/services/spinner.service';
import { VacanciesApiService } from '../services/vacancies-api.service';
import { VacancyInputPopupComponent } from '@vacancies//components/vacancy-input-popup/vacancy-input-popup.component';

@Injectable()
export class VacanciesEffects {
    constructor(
        private readonly actions$: Actions,
        private readonly vacanciesApiService: VacanciesApiService,
        private readonly notificationService: NotificationService,
        private readonly spinnerService: SpinnerService,
        private readonly router: Router,
        private readonly matDialog: MatDialog
    ) { }

    public readonly openVacancyPopup$ = createEffect(() => this.actions$.pipe(
        ofType(vacanciesActions.openVacancyInputPopup),
        switchMap(() => this.matDialog.open(VacancyInputPopupComponent).afterClosed()),
        filter(result => result != null),
        tap(() => this.spinnerService.show()),
        switchMap(description => this.vacanciesApiService.getRecommendations(description)),
        tap(() => {
            this.spinnerService.hide();
            this.router.navigateByUrl('resume-adaptation')
        })
    ));

    public readonly loadJobDescription$ = createEffect(() => this.actions$.pipe(
        ofType(vacanciesActions.loadJobDescription),
        switchMap(({ url }) => this.vacanciesApiService.getDescription(url))
    ));

    public readonly loadVacancies$ = createEffect(() => this.actions$.pipe(
        ofType(vacanciesActions.loadVacancies),
        switchMap(() => this.vacanciesApiService.get())
    ));



    //TODO: add notifications
    // public readonly resetPasswordSuccess$ = createEffect(() =>
    //     this.actions$.pipe(
    //         ofType(authActions.resetPasswordSuccess),
    //         tap(() => this.notificationService.showSuccessMessage(`Link for resetting password was sent`))
    //     ),
    //     { dispatch: false }
    // );
}
