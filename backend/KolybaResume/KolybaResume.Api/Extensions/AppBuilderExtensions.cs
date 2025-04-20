using KolybaResume.DAL.Context;
using Microsoft.EntityFrameworkCore;

namespace KolybaResume.Extensions;

public static class AppBuilderExtensions
{
    public static void UseDBContext(this IApplicationBuilder app)
    {
        using var scope = app.ApplicationServices.GetService<IServiceScopeFactory>()?.CreateScope();
        using var context = scope?.ServiceProvider.GetRequiredService<KolybaResumeContext>();
        context?.Database.Migrate();
    }
}