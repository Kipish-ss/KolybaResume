using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;
using KolybaResume.DAL.Context;

public class KolybaResumeContextFactory : IDesignTimeDbContextFactory<KolybaResumeContext>
{
    public KolybaResumeContext CreateDbContext(string[] args)
    {
        var optionsBuilder = new DbContextOptionsBuilder<KolybaResumeContext>();
        var connectionString = "Host=localhost;Port=5432;Database=kolybaresumedb;Username=postgres;Password=kolyba2025;";

        optionsBuilder.UseNpgsql(connectionString);

        return new KolybaResumeContext(optionsBuilder.Options);
    }
}