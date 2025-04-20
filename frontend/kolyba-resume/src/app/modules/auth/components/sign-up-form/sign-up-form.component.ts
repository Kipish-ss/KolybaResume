import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

import { AuthFormService } from '@auth//services/auth-form.service';
import { AuthService } from '@auth//services/auth.service';
import { AuthStoreService } from '@auth//store/services/auth-store.service';
import { BaseComponent } from '@core/components/base-component/base.component';
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
export class SignUpFormComponent extends BaseComponent {
    public matcher = new PasswordsErrorStateMatcher();

    public hidePassword = true;

    public signUpForm: FormGroup;

    constructor(private authStoreService: AuthStoreService, authService: AuthService) {
        super();
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

    private setCredentialsIncorrect(): void {
        this.signUpForm.get('email')?.setErrors({ incorrectCredentials: true });
        this.signUpForm.get('name')?.setErrors({ incorrectCredentials: true });
        this.signUpForm.get('password')?.setErrors({ incorrectCredentials: true });
    }

    public onSignUp(): void {
        if (this.signUpForm.valid) {
            const email = this.signUpForm.value.email!;
            const password = this.signUpForm.value.password!;
            const name = this.signUpForm.value.name!;

            this.authStoreService.signUp(email, password, name);
        }
    }

    public getEmailErrorMessage(): string {
        if (this.signUpForm.controls['email'].hasError('userAlreadyExists')) {
            return 'An account already exists with this email address';
        }

        return this.signUpForm.controls['email'].invalid ? 'Email format is invalid' : '';
    }

    public userNameChanged(value: string) {
        this.signUpForm.patchValue({ name: removeExcessiveSpaces(value) });
    }
}
