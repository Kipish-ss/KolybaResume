import { AuthCardComponent } from './components/auth-card/auth-card.component';
import { AuthPageComponent } from './components/auth-page/auth-page.component';
import { AuthRoutingModule } from './auth-routing.module';
import { CommonModule } from '@angular/common';
import { ForgotFormComponent } from './components/forgot-form/forgot-form.component';
import { MaterialModule } from '../material-module/material.module';
import { NgModule } from '@angular/core';
import { SignInFormComponent } from './components/sign-in-form/sign-in-form.component';
import { SignUpFormComponent } from './components/sign-up-form/sign-up-form.component';
import { StoreModule } from '@ngrx/store';
import { authReducer } from './store/reducers/auth.reducer';

@NgModule({
    declarations: [
        AuthPageComponent,
        SignInFormComponent,
        SignUpFormComponent,
        ForgotFormComponent,
        AuthCardComponent,
    ],
    imports: [
        CommonModule,
        AuthRoutingModule,
        MaterialModule,
        StoreModule.forFeature('auth', authReducer)
    ],
})
export class AuthModule {}
