import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

import { AuthFormService } from '@auth//services/auth-form.service';
import { AuthService } from '@auth//services/auth.service';
import { AuthStoreService } from '@auth//store/services/auth-store.service';
import { BaseComponent } from '@core/components/base-component/base.component';
import { EmailValidator } from '@auth//validators/email-validator';
import firebase from 'firebase/compat/app';

@Component({
    selector: 'kr-sign-in-form',
    templateUrl: './sign-in-form.component.html',
    styleUrls: ['./sign-in-form.component.sass', '../../shared-styles.sass'],
    standalone: false,
})
export class SignInFormComponent extends BaseComponent implements OnInit {
    public hidePassword = true;

    public signInForm!: FormGroup;

    constructor(private authStoreService: AuthStoreService) {
        super();
    }

    public ngOnInit(): void {
        this.signInForm = new FormGroup(
            {
                email: new FormControl(
                    '',
                    [Validators.required, Validators.email],
                ),
                password: new FormControl('', [Validators.required, Validators.minLength(8)]),
            },
            {
                updateOn: 'blur',
            },
        );
    }

    private setCredentialsIncorrect() {
        this.signInForm.get('password')?.setErrors({ incorrectCredentials: true });
    }

    public onSignIn(): void {
        if (this.signInForm.valid) {
            this.authStoreService.signIn(this.signInForm.value.email!, this.signInForm.value.password!);
        }
    }
}
