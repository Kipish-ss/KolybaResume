import { FormControl, FormGroup, Validators } from '@angular/forms';

import { AuthService } from '@auth//services/auth.service';
import { AuthStoreService } from '@auth//store/services/auth-store.service';
import { Component } from '@angular/core';
import { EmailValidator } from '@auth//validators/email-validator';
import { PasswordsErrorStateMatcher } from '@auth//validators/passwordsErrorStateMatcher';
import { removeExcessiveSpaces } from '@core/helpers/string-helper';
import { userNameRegex } from '@core/constants/model-validation';

@Component({
    selector: 'kr-sign-up-form',
    templateUrl: './sign-up-form.component.html',
    styleUrls: ['./sign-up-form.component.sass', '../../shared-styles.sass'],
    standalone: false,
})
export class SignUpFormComponent {
    public matcher = new PasswordsErrorStateMatcher();

    public hidePassword = true;

    public signUpForm: FormGroup;

    constructor(private authStoreService: AuthStoreService, authService: AuthService) {
        this.signUpForm = new FormGroup({
            email: new FormControl('', {
                validators: [Validators.required, Validators.email],
                asyncValidators: [EmailValidator.signUpEmailValidator(authService)],
                updateOn: 'blur',
            }),
            name: new FormControl('', {
                validators: [
                    Validators.required,
                    Validators.minLength(3),
                    Validators.maxLength(50),
                    Validators.pattern(userNameRegex),
                ],
                updateOn: 'blur',
            }),
            password: new FormControl('', {
                validators: [Validators.required, Validators.minLength(8), Validators.maxLength(30)],
                updateOn: 'blur',
            }),
        });
    }

    public onSignUp(): void {
        if (!this.signUpForm.invalid) {
            const email = this.signUpForm.value.email!;
            const password = this.signUpForm.value.password!;
            const name = this.signUpForm.value.name!;

            this.authStoreService.signUp(email, password, name);
        }
    }

    public getEmailErrorMessage(): string {
        if (this.signUpForm.controls['email'].hasError('userAlreadyExists')) {
            return 'An account already exists with this Email address';
        }

        return this.signUpForm.controls['email'].invalid ? 'Email format is invalid' : '';
    }

    public userNameChanged(value: string) {
        this.signUpForm.patchValue({ name: removeExcessiveSpaces(value) });
    }
}
