using System.Reflection;
using FirebaseAdmin;
using FirebaseAdmin.Auth;
using Google.Apis.Auth.OAuth2;
using KolybaResume.BLL.MappingProfiles;
using KolybaResume.BLL.Services;
using KolybaResume.BLL.Services.Abstract;
using KolybaResume.BLL.Services.Scrappers;
using KolybaResume.DAL.Context;
using KolybaResume.Jobs;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Diagnostics;
using Microsoft.IdentityModel.Tokens;
using Quartz;

namespace KolybaResume.Extensions;

public static class ServiceCollectionExtensions
{
    public static void AddContext(this IServiceCollection services, IConfiguration configuration)
    {
        var connectionsString = configuration.GetConnectionString("KolybaResumeDBConnection");
        services.AddDbContext<KolybaResumeContext>(options =>
            options.UseNpgsql(
                connectionsString,
                opt => opt.MigrationsAssembly(typeof(KolybaResumeContext).Assembly.GetName().Name))
                .ConfigureWarnings(warnings =>
                    warnings.Ignore(
                        RelationalEventId.PendingModelChangesWarning
                    )
                ));
    }

    public static void AddServices(this IServiceCollection services)
    {
        services.AddHttpContextAccessor();
        services.AddHttpClient();
        services.AddScoped<IUserService, UserService>();
        services.AddScoped<IMachineLearningApiService, MachineLearningApiService>();
        services.AddScoped<IVacancyService, VacancyService>();
        services.AddScoped<ICompanyService, CompanyService>();
        services.AddScoped<IDouVacancyAggregatorService, DouVacancyAggregatorService>();
        services.AddScoped<IEmailService, EmailService>();

        services.AddHostedService<ScrapperJob>();
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

    public static void AddQuartz(this IServiceCollection services)
    {
        services.AddQuartz(q =>
        {
            var jobKey = new JobKey("DouJob");

            q.AddJob<DouVacancyJob>(opts => opts
                .WithIdentity(jobKey)
                .StoreDurably());

            q.AddTrigger(opts => opts
                .ForJob(jobKey)
                .WithIdentity("dou-trigger")
                //.WithSimpleSchedule(opt => opt.WithIntervalInHours(24).RepeatForever())
                .WithCronSchedule("0 0 9 * * ?", cronOpts => {
                    cronOpts.InTimeZone(TimeZoneInfo.Local);
                    cronOpts.WithMisfireHandlingInstructionFireAndProceed();
                })
            );
        });

        services.AddQuartzHostedService(options =>
        {
            options.WaitForJobsToComplete = true;
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