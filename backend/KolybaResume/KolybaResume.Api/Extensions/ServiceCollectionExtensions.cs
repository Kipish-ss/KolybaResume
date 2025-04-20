using System.Reflection;
using FirebaseAdmin;
using FirebaseAdmin.Auth;
using Google.Apis.Auth.OAuth2;
using KolybaResume.BLL.MappingProfiles;
using KolybaResume.BLL.Services;
using KolybaResume.DAL.Context;
using KolybaResume.DTO;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;

namespace KolybaResume.Extensions;

public static class ServiceCollectionExtensions
{
    public static void AddContext(this IServiceCollection services, IConfiguration configuration)
    {
        var connectionsString = configuration.GetConnectionString("KolybaResumeDBConnection");
        services.AddDbContext<KolybaResumeContext>(options =>
            options.UseSqlServer(
                connectionsString,
                opt => opt.MigrationsAssembly(typeof(KolybaResumeContext).Assembly.GetName().Name)));
    }

    public static void AddServices(this IServiceCollection services)
    {
        services.AddHttpContextAccessor();
        services.AddTransient<UserService>();
    }
    
    public static void AddAutoMapper(this IServiceCollection services)
    {
        services.AddAutoMapper(Assembly.GetAssembly(typeof(UserProfile)));
    }
    
    public static void ConfigureJwt(this IServiceCollection services, IConfiguration configuration)
    {
        var authority = configuration["Jwt:Firebase:ValidIssuer"];
        var audience = configuration["Jwt:Firebase:ValidAudience"];
        services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
            .AddJwtBearer(options =>
            {
                options.Authority = authority;
                options.TokenValidationParameters = new TokenValidationParameters
                {
                    ValidateIssuer = true,
                    ValidIssuer = authority,
                    ValidateAudience = true,
                    ValidAudience = audience,
                    ValidateLifetime = true
                };
            });
    }
    
    
    
    public static void AddFirebaseAdmin(this IServiceCollection services, IConfiguration configuration)
    {
        var credential = GoogleCredential.FromJson(Environment.GetEnvironmentVariable("FIREBASE_CONFIG_JSON"));
        FirebaseApp.Create(new AppOptions
        {
            Credential = credential
        });

        services.AddTransient<FirebaseAuth>(_ => FirebaseAuth.DefaultInstance);
    }
}