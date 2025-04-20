import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { getAuth, provideAuth } from '@angular/fire/auth';
import { getFirestore, provideFirestore } from '@angular/fire/firestore';
import { initializeApp, provideFirebaseApp } from '@angular/fire/app';
import { provideHttpClient, withInterceptors } from '@angular/common/http';

import { environment } from 'src/environment/environment';
import { errorInterceptorFn } from '@core/interceptors/error.interceptor';
import { jwtInterceptorFn } from '@core/interceptors/jwt.interceptor';
import { provideEffects } from '@ngrx/effects';
import { provideRouter } from '@angular/router';
import { provideStore } from '@ngrx/store';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
    providers: [
        provideZoneChangeDetection({ eventCoalescing: true }),
        provideRouter(routes),
        provideFirebaseApp(() => initializeApp(environment.firebase)),
        provideAuth(() => getAuth()),
        provideFirestore(() => getFirestore()),
        provideHttpClient(
            withInterceptors(
                [
                    jwtInterceptorFn,
                    errorInterceptorFn
                ]
            )
        ),
        provideStore(),
        provideEffects()
    ]
};
