using KolybaResume.DAL.Context.Configurations;
using KolybaResume.DAL.Entities;
using Microsoft.EntityFrameworkCore;

namespace KolybaResume.DAL.Context;

public class KolybaResumeContext(DbContextOptions<KolybaResumeContext> options) : DbContext(options)
{
    public DbSet<User> Users { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfiguration(new UserConfiguration());

        base.OnModelCreating(modelBuilder);
    }
}