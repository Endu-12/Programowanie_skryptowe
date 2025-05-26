<#
  .SYNOPSIS
  Sprawdza kurs podanej waluty wzgledem zlotego

  .DESCRIPTION
  Skrypt wysyla zapytanie do strony nbp.pl spreparowane tak by w odpowiedzi podany byl kurs tej waluty wzgledem zlotowki z ostatnich 5 dni roboczych, oraz sprawdza potem roznice miedzy nimi

  .PARAMETER Waluta
  Parametr odpowiedzialny za sprawdzana walute

  .INPUTS
  Waluta ktora nas interesuje

  .OUTPUTS
  Kurs waluty z 5 dni, oraz roznica miedzy cenami z nastepujacych po sobie dni

  .EXAMPLE
  PS> ./Get-CurrencyRate.ps1 Przykladowa_Waluta

  .EXAMPLE
  PS> ./Get-CurrencyRate.ps1 -Waluta Przykladowa_Waluta

#>

param(
    [Parameter(Mandatory = $true)]
    #Parametr odpowiedzialny za walutę
    [string]$Waluta
)

#Zmienna przechowująca nagłówek mówiący że oczekujemy odpowiedzi w formacie JSON
$Headers = @{ "Accept" = "application/json" }
#Zmienna przechowująca link do strony z której pobieramy informacje
$url = "https://api.nbp.pl/api/exchangerates/rates/A/$Waluta/last/5/?format=json"

#Konstrukcja try catch mająca wychwytywać błędy w zapytaniu
try {
    #Zmienna wysyłająca zapytanie do striny oraz przechowująca jej odpowiedź
    $response = Invoke-RestMethod -Uri $url -Headers $Headers -Method Get
} catch {
    #Error Message
    Write-Host "Blad podczas pobierania danych ze strony"
    exit
}

#Blok mający za zadanie iterowanie po elementach odpowiedzi w celu wypisania kursów walutowych z ostatnich 5 dni wraz z datami
Write-Host "`nKurs waluty $Waluta wzgledem PLN z ostatnich 5 dni:`n"
$rates = $response.rates
foreach ($rate in $rates) {
    Write-Host "$($rate.effectiveDate) : $($rate.mid)"
}

#Blok mający za zadanie iterowanie po elementach odpowiedzi w celu wypisania różnic między kursami walutowymi z ostatnich 5 dni wraz z datami
Write-Host "`nRoznice kursow dzien po dniu:`n"
for ($i = 1; $i -lt $rates.Count; $i++) {
    $pop = $rates[$i - 1].mid
    $obec = $rates[$i].mid
    $roz = [math]::Round($pop - $obec, 4)
    Write-Host "$($rates[$i - 1].effectiveDate) -> $($rates[$i].effectiveDate) : $roz"
}