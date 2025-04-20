import { Component } from '@angular/core';

@Component({
    selector: 'kr-auth-card',
    templateUrl: './auth-card.component.html',
    styleUrls: ['./auth-card.component.sass'],
    standalone: false,
})
export class AuthCardComponent {
    public navLinks = [
        { path: 'sign-in', label: 'Sign In' },
        { path: 'sign-up', label: 'Registration' },
        { path: 'forgot', label: 'Forgot' },
    ];

    public activeTab = this.navLinks[0].label;
}
