using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace KolybaResume.DAL.Migrations
{
    /// <inheritdoc />
    public partial class UpdateSalary : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "SalaryMax",
                table: "Vacancies");

            migrationBuilder.DropColumn(
                name: "SalaryMin",
                table: "Vacancies");

            migrationBuilder.AddColumn<string>(
                name: "Salary",
                table: "Vacancies",
                type: "nvarchar(max)",
                nullable: false,
                defaultValue: "");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Salary",
                table: "Vacancies");

            migrationBuilder.AddColumn<double>(
                name: "SalaryMax",
                table: "Vacancies",
                type: "float",
                nullable: true);

            migrationBuilder.AddColumn<double>(
                name: "SalaryMin",
                table: "Vacancies",
                type: "float",
                nullable: true);
        }
    }
}
