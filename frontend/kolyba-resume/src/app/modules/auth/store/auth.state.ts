import { User } from "../models/user";

export interface AuthState {
    user?: User;
    accessToken?: string;
    emailVerified: boolean
}

export function getAuthInitState(): AuthState {
    return {
        emailVerified: false
    }
}