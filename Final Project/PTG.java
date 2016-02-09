/* Pokemon Team Generator - Generation I
 * Team: Eggy Interactive
 * Members: Brian Lin - bjlin@ucsc.edu
 *          Yunyi Ding - yding13@ucsc.edu
 * AI as "Advisor/Analyst"
 * An Non-Interactive Data Analyst
 * 
 */

import java.util.*;
import java.lang.*;
import java.io.*;

public class PTG{
	private static Hashtable<String,Pokemon> Pokedex;
	private static Hashtable<String,Hashtable<String,Integer>> TypeChart; 
	private static int evolve = 2; //0:minEvolve, 1:random, 2:maxEvolve
	private static String[] types = {"Normal", "Fighting", "Flying", "Poison",
							         "Ground", "Rock", "Bug", "Ghost", "Fire",
	      							 "Water", "Grass", "Electric", "Psychic",
	      							 "Ice", "Dragon"};
	
	public static void main(String[] args){
		importPokemon("pokemon_data.json");
		importTypeChart("type_effectiveness.json");
		
		Pokemon[] Team = new Pokemon[6];
		//Console console = System.console();
		Scanner in = new Scanner(System.in);
		int pokePlace = 0;
		System.out.println("Welcome to the Pokemon Team Generator!\nPlease enter your preferred Pokemon.\nPress enter if you are done.");
		while(pokePlace < 6){
			System.out.print("Preferred Pokemon " + (pokePlace+1) + "> ");
			String name = in.nextLine();
			if(name.length() < 1) break;
			name = name.toLowerCase();
			name = Character.toUpperCase(name.charAt(0)) + name.substring(1);
			Team[pokePlace] = Pokedex.get(name);
			if(Team[pokePlace] != null){
				System.out.println(name + " has successfully been added!");
				pokePlace++;
			}
			else System.out.println("Invalid Pokemon!");
		}
		System.out.println();
		
		Team = generate_team(Team, pokePlace);
		Stats combinedStats = new Stats();
		int[] combinedWeakness = new int[15];
		System.out.println("Pokemon Team:");
		for(int i = 0; i < 6; i++){
			System.out.println(Team[i]);
			combinedStats.addStats(Team[i].get_baseStats());
			for(int j = 0; j < Team[i].get_types().length; j++)
				for(int k = 0; k < 15; k++)
					combinedWeakness[k] += TypeChart.get(Team[i].get_types()[j]).get(types[k]);
		}
		System.out.println("\nTeam Average Base Stats:" + 
						   " hp:" + divide(combinedStats.hp, 6) +
						  " atk:" + divide(combinedStats.atk, 6) +
						  " def:" + divide(combinedStats.def, 6) +
						  " spc:" + divide(combinedStats.spc, 6) +
						  " spe:" + divide(combinedStats.spe, 6) +
						  "\nTeam Type Weakness Rating:");
		for(int i = 0; i < 15; i++)
			System.out.println(types[i] + ":" + combinedWeakness[i]);
	}
	
	private static double divide(double dividend, double divisor){
		return Math.round((dividend*100.0)/divisor)/100.0;
	}
	
	private static Pokemon[] generate_team(Pokemon[] team, int numPokemon){
		for(int i = numPokemon; i < 6; i++){
			switch(evolve){
				case 0: team[i] = maxDevolve(random_pokemon()); break;
				case 1: team[i] = random_pokemon(); break;
				case 2: team[i] = maxEvolve(random_pokemon()); break;
			}
		
			boolean change = false;
			for(int j = 0; j < i; j++){
				if(sameFamily(team[i],team[j])) change = true;
				for(int k = 0; k < team[i].get_types().length; k++)
					for(int l = 0; l < team[j].get_types().length; l++)
						if(team[i].get_types()[k].equals(team[j].get_types()[l]))
							change = true;
				if(change){i--; break;}
			}
		}
		return team;
	}
	
	private static Pokemon maxDevolve(Pokemon p){
		while(!p.get_prevo().equals("none")) p = Pokedex.get(p.get_prevo());
		return p;
	}
	
	private static Pokemon maxEvolve(Pokemon p){
		while(p.get_evos().length > 0)
			p=Pokedex.get(p.get_evos()[(int)(Math.random()*p.get_evos().length)]);
		return p;
	}
	
	private static boolean sameFamily(Pokemon a, Pokemon b){
		if(a.get_name().equals(b.get_name())) return true;
	
		while(!a.get_prevo().equals("none")){
			a = Pokedex.get(a.get_prevo());
			if(a.get_name().equals(b.get_name())) return true;
		}
	
		for(int i = 0; i < a.get_evos().length; i++){
			Pokemon p = Pokedex.get(a.get_evos()[i]);
			if(p.get_name().equals(b.get_name())) return true;
			for(int j = 0; j < p.get_evos().length; j++){
				Pokemon q = Pokedex.get(p.get_evos()[j]);
				if(q.get_name().equals(b.get_name())) return true;
			}
		}
		
		return false;
	}
	
	private static Pokemon random_pokemon(){
		return (Pokemon)Pokedex.values().toArray()[(int)(Math.random()*151)];
	}
	
	private static void print_dex(){
		for(int i = 0; i < Pokedex.values().toArray().length; i++)
			System.out.println(Pokedex.values().toArray()[i]);
	}
	
	private static void importTypeChart(String filepath){
	  TypeChart = new Hashtable<String,Hashtable<String,Integer>>();
	  try{
		Scanner scanner = new Scanner(new File(filepath));
		String currLine = scanner.nextLine();
		for(int i = 0; i < 15; i++){
			currLine = scanner.nextLine();
			currLine = currLine.replace('[',',');
			currLine = currLine.replace(']',',');
			String[] splitLine = currLine.split(",");
			Hashtable<String,Integer> effect = new Hashtable<String,Integer>();
			for(int j = 0; j < 15; j++)
				effect.put(types[j],Integer.parseInt(splitLine[j+1]));
			TypeChart.put(types[i],effect);
		}
	  }catch(IOException e){System.out.println("Error: " + e.getMessage());}
	}
	
	private static void importPokemon(String filepath){
	  Pokedex = new Hashtable<String,Pokemon>();
	  try{
		Scanner scanner = new Scanner(new File(filepath));
		String currLine = scanner.nextLine();
		while(true){
			currLine = scanner.nextLine();
			if(currLine.trim().equals("}")) break;
			
			int searchIndex = currLine.indexOf("species:") + 9;
			String name = currLine.substring(searchIndex, currLine.indexOf("\"", searchIndex));
			
			searchIndex = currLine.indexOf("num:") + 4;
			int index = Integer.parseInt(currLine.substring(searchIndex, currLine.indexOf(",", searchIndex)));
			
			searchIndex = currLine.indexOf("types:") + 7;
			String types_s = currLine.substring(searchIndex, currLine.indexOf("]", searchIndex));
			String[] types = types_s.split(",");
			for(int i=0; i<types.length; i++){
				types[i] = types[i].replace('\"', ' ');
				types[i] = types[i].trim();
			}
			
			searchIndex = currLine.indexOf("baseStats:") + 11;
			String baseStats_s = currLine.substring(searchIndex, currLine.indexOf("}", searchIndex));
			String[] baseStats_a = baseStats_s.split(",");
			int[] baseStats_n = new int[5];
			for(int i = 0; i < 5; i++)
				baseStats_n[i] = Integer.parseInt(baseStats_a[i].substring(baseStats_a[i].indexOf(':')+1).trim());
			Stats baseStats = new Stats(baseStats_n[0],baseStats_n[1],baseStats_n[2],baseStats_n[3],baseStats_n[4]);
			
			searchIndex = currLine.indexOf("prevo:") + 7;
			String prevo = "none";
			if(searchIndex != 6) prevo = currLine.substring(searchIndex, currLine.indexOf("\"", searchIndex));
			
			searchIndex = currLine.indexOf("evos:") + 6;
			String[] evos = new String[0];
			if(searchIndex != 5){
				String evos_s = currLine.substring(searchIndex, currLine.indexOf("]", searchIndex));
				evos = evos_s.split(",");
				for(int i=0; i<evos.length; i++){
					evos[i] = evos[i].replace('\"', ' ');
					evos[i] = evos[i].trim();
				}
			}
			
			Pokedex.put(name, new Pokemon(name, index, types, baseStats, prevo, evos));
		}
	  }catch(IOException e){System.out.println("Error: " + e.getMessage());}
	}
}
	
class Pokemon{
	private String name;
	private int index;
	private String[] types;
	private Stats baseStats;
	private String prevo;
	private String[] evos;
	
	public Pokemon(String n, int i, String[] t, Stats b, String p, String[] e){
		name = n;
		index = i;
		types = t;
		baseStats = b;
		prevo = p;
		evos = e;
	}
		
	public String toString(){
		/*String s = name + ": Index: " + index + "; Type: " + types[0];
		if (types.length == 2) s += ", " + types[1];
		s += "; BaseStats: hp:" + baseStats.hp +
					   ", atk:" + baseStats.atk +
					   ", def:" + baseStats.def +
					   ", spc:" + baseStats.spc +
					   ", spe:" + baseStats.spe +
					   "; Prevo: " + prevo + "; Evos: ";
		for(int i = 0; i < evos.length - 1; i++) s += evos[i] + ", ";
		if (evos.length > 0) s += evos[evos.length - 1];
		else s += "none";*/
		
		String s = name + ": Type: " + types[0];
		if (types.length == 2) s += ", " + types[1];
		s += "; BaseStats: hp:" + baseStats.hp +
						" atk:" + baseStats.atk +
						" def:" + baseStats.def +
						" spc:" + baseStats.spc +
						" spe:" + baseStats.spe;
		return s;
	}
	
	public String get_name(){return name;}
	public int index(){return index;}
	public String[] get_types(){return types;}
	public Stats get_baseStats(){return baseStats;}
	public String get_prevo(){return prevo;}
	public String[] get_evos(){return evos;}
}
	
class Stats{
	public int hp;
	public int atk;
	public int def;
	public int spc;
	public int spe;
	
	public Stats(){
		hp = atk = def = spc = spe = 0;
	}
	
	public Stats(int hp, int atk, int def, int spc, int spe){
		this.hp = hp;
		this.atk = atk;
		this.def = def;
		this.spc = spc;
		this.spe = spe;
	}
	
	public void addStats(Stats s){
		hp += s.hp;
		atk += s.atk;
		def += s.def;
		spc += s.spc;
		spe += s.spe;
	}
}
