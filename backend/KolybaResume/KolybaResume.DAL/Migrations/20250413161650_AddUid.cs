using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace KolybaResume.DAL.Migrations
{
    /// <inheritdoc />
    public partial class AddUid : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "Uid",
                table: "Users",
                type: "nvarchar(450)",
                nullable: false,
                defaultValue: "");

            migrationBuilder.CreateIndex(
                name: "IX_Users_Uid",
                table: "Users",
                column: "Uid",
                unique: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropIndex(
                name: "IX_Users_Uid",
                table: "Users");

            migrationBuilder.DropColumn(
                name: "Uid",
                table: "Users");
        }
    }
}
