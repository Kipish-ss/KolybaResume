import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

import { AuthService } from '@auth//services/auth.service';
import { AuthStoreService } from '@auth//store/services/auth-store.service';
import { EmailValidator } from '@auth//validators/email-validator';
import { Router } from '@angular/router';

@Component({
    selector: 'kr-forgot-form',
    templateUrl: './forgot-form.component.html',
    styleUrls: ['./forgot-form.component.sass', '../../shared-styles.sass'],
    standalone: false,
})
export class ForgotFormComponent implements OnInit {
    public recoveryCode?: number;

    public forgotPasswordForm!: FormGroup;

    constructor(private router: Router, private authService: AuthService, private readonly authStoreService: AuthStoreService) {
    }

    public ngOnInit(): void {
        this.forgotPasswordForm = new FormGroup(
            {
                email: new FormControl(
                    '',
                    [Validators.required, Validators.email],
                    [EmailValidator.loginEmailValidator(this.authService)],
                ),
            },
        );
    }

    public resetPassword(form: FormGroup): void {
        const { email } = form.value;

        this.authStoreService.resetPassword(email)
    }

    public goToSignInPage(): void {
        this.router.navigate(['auth/signin']);
    }
}
