using System.Security.Claims;

namespace KolybaResume.BLL.Extensions;

public static class ClaimsExtensions
{
    
    public static string? GetUid(this ClaimsPrincipal user)
    {
        return user.Claims
            .FirstOrDefault(claim => claim.Type == "user_id")?
            .Value;
    }
}