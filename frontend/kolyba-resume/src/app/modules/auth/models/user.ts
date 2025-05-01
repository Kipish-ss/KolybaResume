import { NewUser } from "./new-user";

export interface User extends NewUser {
    id: number;
    hasResume: boolean;
}